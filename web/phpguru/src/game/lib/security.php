<?php

function sanitize($input) {
    $input = strtolower(urldecode($input));
    
    $WRAPPERS_BLACKLIST = array(
        "file://",
        "ftp://",
        "glob://",
        "phar://",
        "ssh2://",
        "rar://",        
    );
    
    foreach ($WRAPPERS_BLACKLIST as $wrapper) {
        if (str_contains($input, $wrapper)) {
            return "poems/invalid.txt";
        }
    }

    if (str_contains($input, "..")) {
        return "poems/invalid.txt";
    }

    if (filter_var($input, FILTER_VALIDATE_URL)) {
        $url = parse_url($input);
        $ip = gethostbyname($url['host']);
        if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_NO_PRIV_RANGE | FILTER_FLAG_NO_RES_RANGE)) {
            if (isset($url['port'])) {
                return $url['scheme'] . "://" . $url["host"] . ":" . $url['port'] . $url['path'];
            } else {
                return $url['scheme'] . "://" . $url["host"] . $url['path'];
            }
        }
    }

    return "poems/invalid.txt";
}

?>