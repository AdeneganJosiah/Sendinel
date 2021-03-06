#!/bin/sh
cd Sendinel/sendinel || exit 1
python manage.py compilemessages

cd $OLDPWD

# Mac: prevent creation of . files resulting from extended attributes
export COPYFILE_DISABLE=true

tar cvzf Sendinel.tar.gz --exclude='Sendinel/MockUp' \
                         --exclude='Sendinel/Flash' \
                         --exclude='Sendinel/hudson' \
                         --exclude="Sendinel/.git" \
                         --exclude="Sendinel/BluetoothServer" \
                         --exclude="Sendinel/make_package.sh" \
                         --exclude='*.pyc' \
                         --exclude='.DS_Store' \
                         --exclude='.gitignore' \
                         --exclude='Sendinel/sendinel/local_settings.py' \
                         --exclude='sendinel.db' \
                         --exclude='Sendinel/logs' \
                         Sendinel

echo "Done"
