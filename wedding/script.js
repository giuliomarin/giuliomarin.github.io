let collisions = [];
let width = [];
let leftOffSet = [];

// append one event to calendar
var createEvent = (event, height, top, left, units) => {

  let node = document.createElement("div");
  node.className = "event";
  node.innerHTML =
  "<p class='name'>" + event.title + "</p> \
  <p class='location'>" + event.location + "</p>";

  // Customized CSS to position each event
  node.style.width = (92./units) + "%";
  node.style.height = height + "px";
  node.style.top = top + "px";
  node.style.left = left + "%";
  return node;
}

/*
collisions is an array that tells you which events are in each 30 min slot
- each first level of array corresponds to a 30 minute slot on the calendar
- [[0 - 30mins], [ 30 - 60mins], ...]
- next level of array tells you which event is present and the horizontal order
- [0,0,1,2]
==> event 1 is not present, event 2 is not present, event 3 is at order 1, event 4 is at order 2
*/

function getCollisions (events) {

  //resets storage
  collisions = [];

  for (var i = 0; i < 24; i ++) {
    var time = [];
    for (var j = 0; j < events.length; j++) {
      time.push(0);
    }
    collisions.push(time);
  }

  events.forEach((event, id) => {
    let end = event.end;
    let start = event.start;
    let order = 1;

    while (start < end) {
      timeIndex = Math.floor(start/30);

      while (order < events.length) {
        if (collisions[timeIndex].indexOf(order) === -1) {
          break;
        }
        order ++;
      }

      collisions[timeIndex][id] = order;
      start = start + 30;
    }

    collisions[Math.floor((end-1)/30)][id] = order;
  });
};

/*
find width and horizontal position

width - number of units to divide container width by
horizontal position - pixel offset from left
*/
function getAttributes (events) {

  //resets storage
  width = [];
  leftOffSet = [];

  for (var i = 0; i < events.length; i++) {
    width.push(0);
    leftOffSet.push(0);
  }

  collisions.forEach((period) => {

    // number of events in that period
    let count = period.reduce((a,b) => {
      return b ? a + 1 : a;
    })

    if (count > 1) {
      period.forEach((event, id) => {
        // max number of events it is sharing a time period with determines width
        if (period[id]) {
          if (count > width[id]) {
            width[id] = count;
          }
        }

        if (period[id] && !leftOffSet[id]) {
          leftOffSet[id] = period[id];
        }
      })
    }
  });
};

var layOutDay = (events, day, hours) => {

  // clear any existing nodes
  var myNode = document.getElementById(day);
  myNode.innerHTML = '';

  const minutesinDay = 60. * hours;
  const containerHeight = 30. * hours

  getCollisions(events);
  getAttributes(events);

  events.forEach((event, id) => {
    let height = (event.end - event.start) / minutesinDay * containerHeight;
    let top = event.start / minutesinDay * containerHeight;
    let units = width[id];
    if (!units) {units = 1};
    let left = (100.0 / width[id]) * (leftOffSet[id] - 1);
    if (!left || left < 0) {left = 4};
    myNode.appendChild(createEvent(event, height, top, left, units));
  });
}
