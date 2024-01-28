import React, { useState, useRef } from "react";
import Chevron from "./Chevron";

import "./Accordion.css";

function TAccordion(props) {
  const [setActive, setActiveState] = useState("accoractive");
  const [setHeight, setHeightState] = useState("200px");
  const [setRotate, setRotateState] = useState("accordion__icon rotate");

  const content = useRef(null);

  function toggleAccordion() {
    setActiveState(setActive === "" ? "accoractive" : "");
    setHeightState(
      setActive === "accoractive" ? "0px" : `${content.current.scrollHeight}px`
    );
    setRotateState(
      setActive === "accoractive" ? "accordion__icon" : "accordion__icon rotate"
    );
  }


  return (
    <div className="accordion__section">
      <button className={`accordion ${setActive}`} onClick={toggleAccordion}>
        <p className="accordion__title">{props.title}</p>
        <Chevron className={`${setRotate}`} width={10} fill={"#777"} />
      </button>
      <div
        ref={content}
        style={{ maxHeight: `${setHeight}` }}
        className="accordion__content"
      >
        <div
          className="accordion__text"
          dangerouslySetInnerHTML={{ __html: props.content }}
        />
      </div>
    </div>
  );
}

export default TAccordion;
