cd "$(dirname "$0")"

echo Update website Giulio

# Comment lines you don’t want to be executed

scp -r ./*.html maringiu@login.dei.unipd.it:~/Public-Htdocs
#scp -r ./doc/* maringiu@login.dei.unipd.it:~/Public-Htdocs/doc
#scp -r ./images/* maringiu@login.dei.unipd.it:~/Public-Htdocs/images
#scp -r ./publications/* maringiu@login.dei.unipd.it:~/Public-Htdocs/publications
#scp -r ./projects/* maringiu@login.dei.unipd.it:~/Public-Htdocs/projects/
#scp -r ./photos/*.html maringiu@login.dei.unipd.it:~/Public-Htdocs/photos
#scp -r ./extra/*.html maringiu@login.dei.unipd.it:~/Public-Htdocs/extra
#scp -r ./styles/* maringiu@login.dei.unipd.it:~/Public-Htdocs/styles
#scp -r ./scripts/* maringiu@login.dei.unipd.it:~/Public-Htdocs/scripts
