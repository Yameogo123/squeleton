
import React, { useEffect } from 'react';
import './css/App.css';

import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import { useDispatch, useSelector } from 'react-redux';

import moment from 'moment';
import { removeAll } from './hooks/hooks.localStorage';
import { useLocation } from 'react-router-dom';

import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min.js";

import BasicRouting from './routing/routing.basicRouting';
import SecurityRouting from './routing/routing.securityRouting';

function App() {

  const user= useSelector((state)=> state.userReducer.user);
  const limit= useSelector((state)=>state?.userReducer?.limit);
  const dispatch= useDispatch();
  const location= useLocation();

  const logout= ()=>{
    dispatch({type: "logout"});
    removeAll();
  }

  useEffect(()=>{
    const now= moment();
    if(limit && now.diff(moment(limit), "M")>=1){
      logout();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [limit, location])


  return (
    <div className="App">
      {
        user?.nom_complet ? <BasicRouting /> : <SecurityRouting />
      }
      <ToastContainer />
    </div>
  );
}

export default App;
