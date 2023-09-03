from Config import app_name

load_file = """
function load_file(string $path) {
    $path = str_replace('\\\\', '/', $path);
    $in_server = false;
    $rootdir = str_replace('\\\\', '/', $_SERVER['DOCUMENT_ROOT']);
    $rootdirlen = strlen($rootdir);

    if(strncmp($rootdir, $path, $rootdirlen) === 0) {
        $path = substr($path, $rootdirlen);
        $in_server = true;
    }

    $extension = explode('.', basename($path));
    $extlast = array_key_last($extension);
    switch ($path) {
    case 'css':
        load_stylesheet($path, $in_server);
        break;
    
    case 'js':
        load_script($path, $in_server);
        break;
    }

}

function load_stylesheet(string $path, bool $in_server) {
    if($in_server) {
        echo '<link rel=\"stylesheet\" href=\"'.$path.'\">';
    }
    else {
        echo '<style>';
        readfile($path);
        echo '</style>';
    }
}

function load_script(string $path, bool $in_server) {
    if($in_server) {
        echo '<script src=\"'.$path.'\">';
    }
    else {
        echo '<script>';
        readfile($path);
        echo '</script>';
    }
}
"""