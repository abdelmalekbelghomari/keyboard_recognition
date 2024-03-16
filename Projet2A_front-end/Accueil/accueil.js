$(document).ready(function() {
    var text = "Keyboard Acoustic Emanations";
    var index = 0;
    var speed = 100; 

    function typeWriter() {
        if (index < text.length) {
            $("#typing-text").append(text.charAt(index));
            index++;
            setTimeout(typeWriter, speed);
        } else {
            setTimeout(function() {
                window.location.href = "../Transition/hackingMatrixRain.php";
            }, 2000);
        }
    }

    setTimeout(typeWriter, 1500);
});
