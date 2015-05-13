// ==UserScript==
// @name         PHP backtrace clickable links
// @namespace    github.com/webnull
// @version      1.0
// @description  Enables clickable links that will open files in IDE
// @author       Damian Kęska
// @match        http://localhost/*
// @grant        none
// @require      http://code.jquery.com/jquery-latest.js
// ==/UserScript==

xdebugClickableLinks = function () {
    this.serverAddress = 'http://localhost:8161';
    this.linksStyle = 'text-decoration: none; color: black;';
    this.linksAttr = 'target="blank"';
    this.authToken = 'type-your-auth-token-here';
};

xdebugClickableLinks.prototype.openLink = function(link) {
    $.ajax({
        url: this.serverAddress + link,
        beforeSend: function (request)
            {
                request.setRequestHeader("Authority", this.authToken);
            },
        success: function(data) {
            console.log(data);
        }
    });
};

/**
 * Find filesystem paths and append links to them
 *
 * @author Damian Kęska <damian@pantheraframework.org>
 */
xdebugClickableLinks.prototype.parseLinks = function() {
    documentElements = jQuery('.xdebug-error');
    
    if (documentElements.length)
    {
        elements = jQuery('.xdebug-error td[title]');
        var t = this;
        
        /**
         * Find paths in "location" column"
         */
        elements.each(function (key, element) {
            element = jQuery(element);
            lineNumber = element.html().split('</b>')[1];
            element.html('<a href="javascript:window.xdebugClickableLinks.openLink(\'/open-project-file/' + btoa(element.attr('title')) + '/' + lineNumber + '\');" ' + t.linksAttr+ ' style="' + t.linksStyle + '">' + element.html() + '</a>');
        }); 
        
        /**
         * Find possible paths in messages
         */
        elements = jQuery('.xdebug-error th[colspan]');
        elements.each(function (key, element) {
            element = jQuery(element);
            
            re = /in ([A-Z\/a-z0-9\-\.]+) on line \<i\>([0-9]+)\<\/i\>/g; 
            tmp = re.exec(element.html());
            
            if (tmp)
            {
                element.html(element.html().replace(tmp[1], '<a href="javascript:window.xdebugClickableLinks.openLink(\'/open-project-file/' + btoa(tmp[1]) + '/' + tmp[2] + '/\');" ' + t.linksAttr+ ' style="' + t.linksStyle + '">' + tmp[1] + '</a>'));
            }
        });
    }
};

jQuery(document).ready(function() {
    window.xdebugClickableLinks = new xdebugClickableLinks();
    window.xdebugClickableLinks.parseLinks();
});
