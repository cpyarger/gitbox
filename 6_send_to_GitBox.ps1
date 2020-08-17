Get-ChildItem Files | ForEach-Object {

cd "$($_.FullName)"
git init
$hello = "BOSI/$($_.Name)"
$hello | Out-File ./repo.txt -Encoding ASCII
cp "$($_.Name).html"  index.html
git add -A

git commit -am "initial commit"
git remote remove remote
git remote add remote git@gitbox.org:BOSI/"$($_.Name).git"
git push --force -u remote master

}
cd ..\..
