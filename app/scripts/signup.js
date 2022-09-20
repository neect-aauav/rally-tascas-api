const addCourses = (select, courses) => {
    courses.forEach(course => {
        const option = document.createElement("option");
        select.appendChild(option);
        option.appendChild(document.createTextNode(course));
    });
}

const courses_list = new Set(UA_COURSES.sort((a, b) => a.localeCompare(b)));

const memberSelects = document.querySelectorAll(".members select");
memberSelects.forEach(select => addCourses(select, courses_list));

let memberCounter = 1;
memberInput = () => {
    const wrapper = document.createElement("div");
    
    const name = document.createElement("input");
    wrapper.appendChild(name);
    name.placeholder = "Nome";
    name.type = "text";
    name.name = `member[${memberCounter}]`;
    name.required = true;
    
    const nmec = document.createElement("input");
    wrapper.appendChild(nmec);
    nmec.classList.add("nmec-input");
    nmec.placeholder = "NMEC";
    nmec.type = "text";
    nmec.name = `nmec[${memberCounter}]`;
    nmec.required = true;
    
    const courses = document.createElement("select");
    wrapper.appendChild(courses);
    courses.name = `course[${memberCounter}]`;
    courses.required = true;
    addCourses(courses, ["", ...courses_list]);
    
    wrapper.appendChild(removeMemberCross(() => {
        if (++memberCounter <= 1)
            document.querySelector(".remove-member").classList.replace("clickable", "inactive");
    }));

    return wrapper;
}

const addMember = document.querySelector(".add-member");
const members = document.querySelector(".members");
if (addMember) {
    addMember.addEventListener("click", () => {
        if (memberCounter < 10) {
            members.insertBefore(memberInput(), addMember);
            insertUrlParam("members", memberCounter);
            if (memberCounter > 1)
                document.querySelector(".remove-member").classList.replace("inactive", "clickable");
            
            if (memberCounter == 10) addMember.classList.add("hidden");
        }
    });
}

const removeMemberCross = callback => {
    const wrapper = document.createElement("div");
    wrapper.classList.add("remove-member", "clickable");
    const crossWrapper = document.createElement("div");
    crossWrapper.classList.add("absolute-centered");
    wrapper.appendChild(crossWrapper);
    for (let i = 0; i < 2; i++) {
        crossWrapper.appendChild(document.createElement("div"));
    }
    wrapper.addEventListener("click", () => {
        if (memberCounter > 1) {
            wrapper.parentElement.remove();
            insertUrlParam("members", --memberCounter);
        }

        if (memberCounter == 9) addMember.classList.remove("hidden");

        if (callback) callback();
    });

    return wrapper;
}

document.addEventListener("input", e => {
    const target = e.target;

    if (target.classList.contains("nmec-input")) {
        if (target.value.length > 6) target.value = target.value.slice(0, -1);
    }

    if (target.closest(".team input[type='text']"))
        insertUrlParam("team", target.closest(".team input[type='text']").value);

    if (target.closest(".team input[type='email']"))
        insertUrlParam("email", target.closest(".team input[type='email']").value);
});

const insertUrlParam = (key, value) => {
	let searchParams = new URLSearchParams(window.location.search);
	searchParams.set(key, value);
	let newurl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + searchParams.toString();
	window.history.replaceState({}, '', newurl);
}

const urlParams = new URLSearchParams(window.location.search);
if (urlParams.get('team'))
    document.querySelector("input[type='text']").value = urlParams.get('team');

if (urlParams.get('email'))
    document.querySelector("input[type='email']").value = urlParams.get('email');

if (urlParams.get('members')) {
    let nMembers = Number(urlParams.get('members'));
    if (nMembers < 1) nMembers = 1;
    if (nMembers > 10) nMembers = 10;

    insertUrlParam("members", nMembers);

    document.querySelector(".remove-member").classList.replace("inactive", "clickable");

    for (let i = 1; i < nMembers; i++) {
        members.insertBefore(memberInput(), addMember)
    }

    if (memberCounter == 1) document.querySelector(".remove-member").classList.replace("clickable", "inactive");
    if (memberCounter == 10) addMember.classList.add("hidden");
}