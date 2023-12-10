(function() {
    includeHTML();

    function includeHTML() {
        var elements, i, element, includeHTMLAttribute, xmlHttpRequest;
        elements = document.getElementsByTagName("*");

        for (i = 0; i < elements.length; i++) {
            element = elements[i];
            includeHTMLAttribute = element.getAttribute("include-html");

            if (includeHTMLAttribute) {
                xmlHttpRequest = new XMLHttpRequest();

                xmlHttpRequest.onreadystatechange = function() {
                    // readyState: 0:UNSENT, 1:OPENED, 2:HEADERS_RECEIVED, 3:LOADING, 4:DONE
                    // https://developer.mozilla.org/en-US/docs/Web/API/XMLHttpRequest/readyState
                    if (xmlHttpRequest.readyState == 4) {
                        // status: 200:OK, 404:Not Found
                        // https://developer.mozilla.org/en-US/docs/Web/HTTP/Status
                        if (xmlHttpRequest.status == 200) {element.innerHTML = xmlHttpRequest.responseText;}
                        if (xmlHttpRequest.status == 404) {element.innerHTML = "Page not found.";}
                        element.removeAttribute("include-html");
                        includeHTML();
                    }
                }

                xmlHttpRequest.open("GET", includeHTMLAttribute, true);
                xmlHttpRequest.send();
                return;
            }
        }
    }
})();