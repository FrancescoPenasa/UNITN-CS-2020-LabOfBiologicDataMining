<?php
 if(!empty($argv[1])) {
    $name = $argv[1];
  } else {
    echo "usage: $argv[0] gene\n";
    exit;
  }
  $look = "grep -P '\t".$name."$' z_codes.txt";

#  echo $look, "\n";
  exec($look, $list);
#  print_r($list);
  foreach($list as $i) {
    list($id, $coord, $foo) = explode("\t", $i);
 #   echo $id, ' ', $coord,"\n";
    $file = $id.'-'.$name.'.lgn';
    echo $file, '(',$coord,')',"\n";
    $fw = fopen($file, 'w');
    fwrite($fw, "from,to\n$id,$id\n");
    fclose($fw);
  }

?>
