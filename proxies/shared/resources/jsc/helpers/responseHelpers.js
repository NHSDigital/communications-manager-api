const replacePathRoot = (baseUrl, link) => {
    const withoutPathRoot = link.replace("%PATH_ROOT%", "").split("").reverse().join("");
    if (baseUrl.split("").reverse().join("").indexOf(withoutPathRoot) === 0) {
        return baseUrl;
    } 
        return link.replace("%PATH_ROOT%", baseUrl);
    
}
