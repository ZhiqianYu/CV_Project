function loadVideoAnnotations() {
    // 获取选定的视频 ID
    var selectedVideoId = document.getElementById("videoSelect").value;

    // 构建新的 URL，将选定的视频 ID 作为查询参数
    var newUrl = "/exportpage/select/" + selectedVideoId + "/";

    // 重定向到新的 URL
    window.location.href = newUrl;
}