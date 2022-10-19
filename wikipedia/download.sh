languages="de en fr"
for language in $languages do
    wget --content-disposition "https://download.kiwix.org/zim/wikipedia_${language}_all_nopic.zim"
done