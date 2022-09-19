const addCourses = (select, courses) => {
    courses.forEach(course => {
        const option = document.createElement("option");
        select.appendChild(option);
        option.appendChild(document.createTextNode(course));
    });
}

const memberSelects = document.querySelectorAll(".members select");
memberSelects.forEach(select => addCourses(select, UA_COURSES));

memberInput = () => {
    const wrapper = document.createElement("div");
    const name = document.createElement("input");
    wrapper.appendChild(name);
    name.placeholder = "Nome";
    name.type = "text";
    name.name = "member";
    const courses = document.createElement("select");
    wrapper.appendChild(courses);
    addCourses(courses, ["", ...UA_COURSES]);
    return wrapper;
}

const addMember = document.querySelector(".add-member");
if (addMember) {
    addMember.addEventListener("click", () => {
        const members = document.querySelector(".members");
        members.insertBefore(memberInput(), addMember);
    });
}