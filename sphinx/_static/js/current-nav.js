 document.addEventListener("DOMContentLoaded", function() {
    // Initialization: wait for window load and then trigger current nav detection.
    window.addEventListener("load", function() {
      console.log("Window loaded, initializing current nav...");
      initCurrentNav();
    });
  
    // Re-trigger when the hash changes.
    window.addEventListener("hashchange", function() {
      console.log("Hash changed, reinitializing current nav...");
      initCurrentNav();
    });
  
    function initCurrentNav() {
      // If Alpine.js is available and provides nextTick, use it.
      if (window.Alpine && typeof window.Alpine.nextTick === 'function') {
        window.Alpine.nextTick(processNav);
      } else {
        processNav();
      }
    }
  
    function processNav() {
      var currentHash = window.location.hash;
      console.log("initCurrentNav: Current hash:", currentHash);
      if (!currentHash) return;
      
      // Select all internal links within the .current-index container.
      var links = document.querySelectorAll('.current-index a.reference.internal');
      links.forEach(function(link) {
        var href = link.getAttribute("href");
        console.log("initCurrentNav: Checking link:", href);
        // If the link is hash-only (e.g. "#setup-guide")
        if (href && href.trim().startsWith("#")) {
          if (href.trim() === currentHash.trim()) {
            console.log("initCurrentNav: Match found for hash-only link:", href);
            document.querySelectorAll('.current-index a.reference.internal.current').forEach(function(link) {
              link.classList.remove("current");
            });            
            link.classList.add("current");
            markAsCurrent(link);
          }
        }
        // Otherwise, if the link includes a file and a hash, compare the hash part.
        else if (href && href.indexOf('#') !== -1) {
          var parts = href.split('#');
          var linkHash = "#" + parts[1].trim();
          console.log("initCurrentNav: Extracted link hash:", linkHash);
          if (linkHash === currentHash.trim()) {
            console.log("initCurrentNav: Match found for link with file and hash:", href);
            markAsCurrent(link);
          }
        }
        else {
          console.log("initCurrentNav: No match for link:", href);
        }
      });
      
      // After processing links, open submenus only for those li elements marked as current.
      openCurrentSubmenus();
    }
  
    // Mark the link's parent li and all its ancestor li elements as current.
    function markAsCurrent(link) {
      var li = link.closest("li");
      if (!li) {
        console.log("markAsCurrent: No parent li found for link:", link);
        return;
      }
      li.classList.add("current");
      console.log("markAsCurrent: Marked li as current:", li);
      // If Alpine.js is used, set its "expanded" property to true.
      if (li.__x && li.__x.$data) {
        li.__x.$data.expanded = true;
        console.log("markAsCurrent: Set Alpine expanded on li:", li);
      }
      // Propagate upward: mark all ancestor li elements as current.
      var parentLi = li.parentElement.closest("li");
      while (parentLi) {
        parentLi.classList.add("current");
        if (parentLi.__x && parentLi.__x.$data) {
          parentLi.__x.$data.expanded = true;
        }
        console.log("markAsCurrent: Propagated current to ancestor li:", parentLi);
        parentLi = parentLi.parentElement.closest("li");
      }
    }
  
    // Open immediate submenu elements (the direct children with x-show) of li.current.
    function openCurrentSubmenus() {
      document.querySelectorAll('.current-index li.current').forEach(function(li) {
        // Only target immediate child elements that have x-show.
        li.querySelectorAll(":scope > [x-show]").forEach(function(elem) {
          if (elem.style.display === "none" || elem.style.display === "") {
            elem.style.display = "block";
            console.log("openCurrentSubmenus: Opened submenu element:", elem);
          }
        });
      });
    }
    window.initCurrentNav = initCurrentNav;
  });
