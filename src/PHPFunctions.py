from Config import app_name

load_file = """
function load_file(string $initial_path, string $file_options = '', string $content_options = '') {
    $path = str_replace('\\\\', '/', $initial_path);
    $in_server = false;
    $rootdir = str_replace('\\\\', '/', $_SERVER['DOCUMENT_ROOT']);
    $rootdirlen = strlen($rootdir);

    if(strncmp($rootdir, $path, $rootdirlen) === 0) {
        $path = substr($path, $rootdirlen);
        $in_server = true;
    }

    $extension = explode('.', basename($path));
    $extlast = array_key_last($extension);
    if($extlast !== null) {
        switch ($extension[$extlast]) {
        case 'css':
            load_stylesheet($path, $in_server, $file_options, $content_options);
            break;
    
        case 'js':
            load_script($path, $in_server, $file_options, $content_options);
            break;
        
        case 'svg':
            load_svg($initial_path);
            break;
        }
    }

}

function load_stylesheet(string $path, bool $in_server, string $file_options, string $content_options) {
    if($in_server) {
        echo '<link rel=\"stylesheet\" href=\"'.$path.'\" '.$file_options.'>';
    }
    else {
        echo '<style '.$content_options.'>';
        readfile($path);
        echo '</style>';
    }
}

function load_script(string $path, bool $in_server, string $file_options, string $content_options) {
    if($in_server) {
        echo '<script src=\"'.$path.'\" '.$file_options.'></script>';
    }
    else {
        echo '<script '.$content_options.'>';
        readfile($path);
        echo '</script>';
    }
}

function load_svg(string $path) {
    readfile($path);
}
"""