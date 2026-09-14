(() => {
  const dialog = document.querySelector("[data-search-dialog]");
  const toggles = [...document.querySelectorAll("[data-search-toggle]")];
  const closeButton = document.querySelector("[data-search-close]");
  let initialized = false;
  let returnFocus = null;

  const initializeSearch = () => {
    if (initialized || typeof PagefindUI === "undefined") return;
    new PagefindUI({
      element: "#search",
      showSubResults: true,
      showImages: false,
      translations: {
        placeholder: "搜索章节、概念与系统",
        clear_search: "清除",
        load_more: "加载更多结果",
        search_label: "搜索全书",
        filters_label: "筛选",
        zero_results: "没有找到“[SEARCH_TERM]”",
        many_results: "找到 [COUNT] 条“[SEARCH_TERM]”相关结果",
        one_result: "找到 1 条“[SEARCH_TERM]”相关结果",
        alt_search: "没有找到“[SEARCH_TERM]”。显示“[DIFFERENT_TERM]”的结果",
        search_suggestion: "没有找到“[SEARCH_TERM]”。可以尝试：",
        searching: "正在搜索“[SEARCH_TERM]”…",
      },
    });
    initialized = true;
  };

  const openSearch = (toggle) => {
    if (!dialog) return;
    returnFocus = toggle;
    initializeSearch();
    dialog.showModal();
    toggles.forEach((button) => button.setAttribute("aria-expanded", "true"));
    window.setTimeout(() => dialog.querySelector("input")?.focus(), 0);
  };

  const closeSearch = () => {
    if (!dialog?.open) return;
    dialog.close();
  };

  toggles.forEach((toggle) => toggle.addEventListener("click", () => openSearch(toggle)));
  closeButton?.addEventListener("click", closeSearch);
  dialog?.addEventListener("click", (event) => {
    if (event.target === dialog) closeSearch();
  });
  dialog?.addEventListener("close", () => {
    toggles.forEach((button) => button.setAttribute("aria-expanded", "false"));
    returnFocus?.focus();
  });
  document.addEventListener("keydown", (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault();
      if (dialog?.open) closeSearch();
      else openSearch(toggles[0]);
    } else if (event.key === "Escape" && dialog?.open) {
      closeSearch();
    }
  });
})();
