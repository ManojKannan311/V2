$("#D_Broucher_category").change(function () {
    var categoryId = $(this).val();
    var subcategoryDropdown = $("#D_Broucher_subcategory");
    var subcategoryContainer = $("#D_Broucher_subcategory-container");

    console.log("Selected Category ID:", categoryId);

    if (categoryId) {
        $.ajax({
            url: `/gEt_sub_cat/${categoryId}/`,
            type: "GET",
            success: function (data) {
                console.log("AJAX Response:", data);

                subcategoryDropdown.empty().append('<option selected disabled>Choose...</option>');

                if (data.sub && data.sub.length > 0) {
                    $.each(data.sub, function (index, sub) {
                        console.log("Appending subcategory:", sub.name);
                        subcategoryDropdown.append(`<option value="${sub.id}">${sub.name}</option>`);
                    });
                } else {
                    console.log("No subcategories found!");
                }
            },
            error: function (xhr, status, error) {
                console.log("Error fetching subcategories:", error);
                alert("Error fetching subcategories! Check console for details.");
            }
        });
    } else {
        subcategoryContainer.addClass("d-none"); // Hide if no category is selected
    }
});
