const taskList = document.querySelector("ol");
const tasks = document.querySelectorAll("[data-task-id]");

//tworzy zmienną, w której zapamiętujemy aktualnie przeciągany task
let draggedTask = null;

for (const task of tasks) {
    task.draggable = true;

    task.addEventListener("dragstart", function () {
//        po rozpoczęciu przeciąganie zapisujemy konkretny element <li>
        draggedTask = task;
    });
    task.addEventListener("dragover", function(event) {
//        Pozwala upuszczać element. Bez tego przeglądarka blokuje standardową obsługę dragover
        event.preventDefault();

//sprawdza czy task nad którym aktualnie znajduje się kursor, nie jest tym samym taskiem, który przeciągasz.
        if (task !== draggedTask) {
//        ta metoda pobiera informacje o położeniu i rozmiarze elementu na ekranie
            const taskRectangle = task.getBoundingClientRect();
//            wyliczamy środek taska w pionie
            const taskMiddle = taskRectangle.top + taskRectangle.height / 2;
//          oznacza pionową pozycję kursora myszy na ekranie (pozycja kursora < środek taska)
            if (event.clientY < taskMiddle) {
//            wstaw draggedtask do tasklist przed elementem task
                taskList.insertBefore(draggedTask, task);
            } else {
//            Jeżeli kursor jest nad górną połową taska, wstaw przeciągany element przed nim, a jeżeli nad dolną połową — wstaw go przed następnym elementem, czyli faktycznie za nim.
                taskList.insertBefore(draggedTask, task.nextSibling);
            }
        }
    });
}