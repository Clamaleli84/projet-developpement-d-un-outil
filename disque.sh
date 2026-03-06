#/bin/bash

function memory(){
  free | awk '/Mem:/ {printf("Utilisation de la Mémoire : %.2f%%\n", $3/$2 * 100)}'
  }
