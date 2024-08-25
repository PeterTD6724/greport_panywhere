document.addEventListener("DOMContentLoaded", function ()
{
    const nameSearch = document.getElementById("name-search")
    const tags = document.querySelectorAll(".tag")
    const projects = document.querySelectorAll(".time")

    function filterProjects()
    {
        const nameQuery = nameSearch.value.toLowerCase();

        projects.forEach((project) =>
        {
            const name = project.getAttribute('data-name')
            const nameMatch = name.includes(nameQuery)

            if (nameMatch)
            {
                project.style.display = "";
            } else
            {
                project.style.display = "none";
            }
        })
    }

    nameSearch.addEventListener("keyup", filterProjects)
})


// document.addEventListener("DOMContentLoaded", function ()
// {
//     const nameSearch = document.getElementById("name-search");
//     const tags = document.querySelectorAll(".tag");
//     const projects = document.querySelectorAll(".time");

//     if (!nameSearch)
//     {
//         console.error('Element with id "name-search" not found in the DOM.');
//         return;
//     }

//     function filterProjects()
//     {
//         const nameQuery = nameSearch.value.toLowerCase();

//         projects.forEach((project) =>
//         {
//             const name = project.getAttribute('data-name');
//             const nameMatch = name.includes(nameQuery);

//             project.style.display = nameMatch ? "" : "none";
//         });
//     }

//     nameSearch.addEventListener("keyup", filterProjects);
// });