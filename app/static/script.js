document.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("tbody tr");
    const searchInput = document.getElementById("searchInput");

    rows.forEach(row => {
        row.addEventListener("click", () => {
            const id = row.querySelector("a")?.getAttribute("href")?.split("/").pop();
            if (id) {
                window.location.href = `/regions/${id}`;
            }
        });
    });

    searchInput?.addEventListener("input", (e) => {
        const keyword = e.target.value.toLowerCase();
        rows.forEach(row => {
            const name = row.cells[0].innerText.toLowerCase();
            row.style.display = name.includes(keyword) ? "" : "none";
        });
    });

    // 지역 추가 폼
    const addForm = document.getElementById("addForm");
    if (addForm) {
        addForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(addForm);
            const data = Object.fromEntries(formData.entries());
            data.housing_price = Number(data.housing_price);
            data.transport_score = Number(data.transport_score);
            data.safety_score = Number(data.safety_score);
            data.environment_score = Number(data.environment_score);
            data.score = Number(data.score);
            const res = await fetch("/regions/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            if (res.ok) location.reload();
            else alert("추가 실패");
        });
    }

    // 삭제 버튼
    const deleteBtns = document.querySelectorAll(".delete-btn");
    deleteBtns.forEach(btn => {
        btn.addEventListener("click", async (e) => {
            e.stopPropagation();
            const id = btn.dataset.id;
            if (confirm("정말 삭제하시겠습니까?")) {
                const res = await fetch(`/regions/${id}`, { method: "DELETE" });
                if (res.ok) location.reload();
                else alert("삭제 실패");
            }
        });
    });

    // 상세 페이지 수정/삭제
    const editForm = document.getElementById("editForm");
    if (editForm) {
        editForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const formData = new FormData(editForm);
            const data = Object.fromEntries(formData.entries());
            data.housing_price = Number(data.housing_price);
            data.transport_score = Number(data.transport_score);
            data.safety_score = Number(data.safety_score);
            data.environment_score = Number(data.environment_score);
            const id = window.location.pathname.split("/").pop();
            const res = await fetch(`/regions/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(data)
            });
            if (res.ok) location.reload();
            else alert("수정 실패");
        });
        document.getElementById("deleteBtn").addEventListener("click", async () => {
            const id = window.location.pathname.split("/").pop();
            if (confirm("정말 삭제하시겠습니까?")) {
                const res = await fetch(`/regions/${id}`, { method: "DELETE" });
                if (res.ok) window.location.href = "/";
                else alert("삭제 실패");
            }
        });
    }
});