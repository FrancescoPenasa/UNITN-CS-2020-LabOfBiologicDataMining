<?php
 if(!empty($argv[1])) {
    $name = $argv[1];
  } else {
    echo "usage: $argv[0] gene\n";
    exit;
  }

  $look = "awk '{print $1 \"|\" $4}' r_anno.txt |grep '@".$name.'$\'';
 echo $look, "\n";
  exec($look, $list);
#  print_r($list);
  foreach($list as $i) {
    list($coord, $p) = explode('|',$i);
    $id = exec("grep $coord transcripts_id_mapping.tsv | cut -f 1");
    $file = $id.'-'.$name.'.lgn';
    echo $file, '(',$coord,')',"\n";
    $fw = fopen($file, 'w');
    fwrite($fw, "from,to\n$id,$id\n");
    fclose($fw);
  }

?>
