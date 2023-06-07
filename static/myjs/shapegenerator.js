let shapesList = shapes;

function generateShapes(element = document.body, colorList = ["#a29bfe","#ffeaa7","#ff7675"], numberOfShapes = 5, shapesMode = 2, rotation = false) {
    let newElement = document.createElement("div");

    let rotationList = ["rotate(0deg)", "rotate(45deg)", "rotate(90deg)", "rotate(125deg)", "rotate(180deg)", "rotate(270deg)"];

    newElement.style.width = element.clientWidth + "px";
    newElement.style.height = element.clientHeight + "px";
    newElement.style.position = "absolute";
    newElement.style.zIndex = -1;
    newElement.style.top = 0;
    newElement.style.left = 0;
    element.appendChild(newElement);
    for (let i = 0; i < numberOfShapes; i++) {
        let shape = shapesList[Math.floor(Math.random() * shapesList.length)];
        let color = colorList[Math.floor(Math.random() * colorList.length)];
        let top = Math.floor(Math.random() * element.clientHeight);
        let left = Math.floor(Math.random() * element.clientWidth);
        let width = Math.floor(Math.random() * 100);
        let height = Math.floor(Math.random() * 100);
        let shapeElement = document.createElement("div");
        shapeElement.id = "shape"+i;
        shapeElement.style.position = "absolute";
        shapeElement.style.top = top + "px";
        shapeElement.style.left =left + "px";


        if (shapesMode == 1) {
            shapeElement.style.width = width + "px";
            shapeElement.style.height = height + "px";
            shapeElement.style.backgroundColor = color;
            shapeElement.style.clipPath = shape;
        }
        shapeElement.innerHTML = shape;
        if (rotation) {
            shapeElement.style.transform = rotationList[Math.floor(Math.random() * rotationList.length)];
        }
        newElement.appendChild(shapeElement);


        // console.log(shapesMode);
        if (shapesMode == 2) {
            let svgElementsList =    [" line", " circle", " path", " rect"];
            for (let k = 0; k < svgElementsList.length; k++) {
                let svgElement = svgElementsList[k];
                let ElementsList = document.querySelectorAll("#shape"+i+" svg"+svgElement);
                for (let j = 0; j < ElementsList.length; j++) {
                    let element = ElementsList[j];
                    // check if the element is has a fill or stroke attribute
                    // if it has a fill or stroke attribute then change it to the color

                    if (element.hasAttribute("fill")) {
                        element.setAttribute("fill", color);
                    }
                    if (element.hasAttribute("stroke")) {
                        element.setAttribute("stroke", color);
                    }
                }
                
            }
        }
    }
}

