#!/bin/bash


#root='/Users/edison/Dropbox/Avocado/core'
root='/tmp/static/'


Uglifyjs='/usr/local/bin/node /usr/local/bin/uglifyjs'
CleanCss='/usr/local/bin/node /usr/local/bin/cleancss'
ComboCss='/usr/local/bin/node /usr/local/bin/csscombo'




#echo "*** css and js version ***"
#ver=`date '+%Y%m%d %H:%M:%S'|md5`;
#echo $ver;

cd $root

echo "*** compress js ***";
#cd scripts/
#find . -type f -name '*.js' -exec bash -c "${Uglifyjs} {} > {}.tmp; mv -f {}.tmp {}" \;
#mkdir $ver
#find . -type f -name '*.js' -exec cp {} $ver \;

#mkdir static/management/js/$ver
#cp static/management/js/*.js static/management/js/$ver

echo "*** compress css ***";
cd styles/
CssList=$(find . -type f -name '*.css' -exec basename {} \;)
for css in $CssList
do
    ${ComboCss} $css combo.$css
    ${CleanCss} combo.$css > $css
    rm -f combo.$css
done
