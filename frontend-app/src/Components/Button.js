import React from "react";
import "../styles/Button.css"; // Import the new CSS file

function Button({ name, onClick, icon, bg, type, disabled }) {
  return (
    <button
      className="button"
      style={{ background: bg }}
      onClick={onClick}
      type={type}
      disabled={disabled}
    >
      {icon}
      {name}
    </button>
  );
}

export default Button;
