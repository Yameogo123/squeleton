

import React from "react";

import { Route, Routes } from "react-router-dom";
//import { useSelector } from "react-redux";
import Home from "../views/view.home";


export default function BasicRouting() {

    //const user = useSelector((state)=> state.userReducer.user);

    return (
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="*" element={<Home />} /> 
        </Routes>
    )
}

