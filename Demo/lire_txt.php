<?php
if (isset($_POST['mode'])){
    $mode_utilisateur = $_POST['mode'];

    if ($mode_utilisateur == 'true'){
        $chemin_fichier = '../models_results/person_results.txt';
    } else {
        $chemin_fichier = '../models_results/letter_results.txt';
    }

    $fichier = fopen($chemin_fichier, 'r');
    if ($fichier) {
        $premiere_ligne = fgets($fichier);
        fclose($fichier);
        $data = array('line' => $premiere_ligne);
        $json_data = json_encode($data);
        echo $json_data;
    } else {
        echo json_encode(array('error' => 'Impossible d\'ouvrir le fichier'));
    }
}
?>
