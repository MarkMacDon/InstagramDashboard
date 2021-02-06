import React from 'react'
import ReactDOM from 'react-dom'
import PasswordRegexChecks from './passwordregexchecks.js'

function Welcome(props) {
  return <h1>Hello, {props.name}</h1>;
}

const element = <Welcome name="world" />;
const secondelement = <PasswordRegexChecks password="t@@#sSS1est" />
ReactDOM.render(
  secondelement,
  document.getElementById('react')
);
ReactDOM.render(
  element,
  document.getElementById('react1')
);
