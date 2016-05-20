#! /bin/bash

# renew lease
krenew

# Download page from google scholar

wget -O - "https://scholar.google.com/citations?user=t9UpeEAAAAAJ&hl=en" > /home/maringiu/Public-Htdocs/publications/googlescholar_giuliomarin.html

wget -O - "https://www.runtastic.com/en/users/Giulio-Marin/statistics" > /home/maringiu/Public-Htdocs/extra/runtastic_giuliomarin.html
