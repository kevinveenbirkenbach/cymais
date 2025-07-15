# Administration

## DANGER: Manuell deativation and deletion
Be carefull what you do. This code you can execute:
```
systemctl list-units --type=service | grep 'matrix' | awk '{print $1}' | xargs -I {} systemctl disable {} &&
systemctl list-units --type=service | grep 'matrix' | awk '{print $1}' | xargs -I {} systemctl stop {} &&
rm -rv /matrix/
```