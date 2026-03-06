#/bin/bash
  free | awk '/Mem:/ {printf("Utilisation de la RAM : %.2f%%\n", $3/$2 * 100)}'
