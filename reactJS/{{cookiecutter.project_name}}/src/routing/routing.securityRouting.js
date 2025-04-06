

import React from "react";
import { Route, Routes } from "react-router-dom";
import Login from "../views/security/login";



export default function SecurityRouting() {

    return (
        <Routes>
            <Route path="/" element={<Login />} />
            <Route path="*" element={<Login />} /> 
        </Routes>
    )
}

