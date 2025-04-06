
import React, { useState } from "react";
import { getInputedValue, reloadPage } from "../../controllers/controller.utils";
import { handleLogin } from "../../controllers/controller.user";
import { useDispatch } from "react-redux";

export default function Login() {

    const [email, setEmail] = useState('');
    const [pwd, setPwd] = useState('');
    const [disable, setDisable] = useState(false);
    const dispatch = useDispatch();

    async function login(e) {
        e.preventDefault();
        setDisable(true);
        let res = await handleLogin(e, email, pwd);
        if (res !== -1) {
            dispatch(res);
            reloadPage();
        }
        setDisable(false);
    }

    return (
        <div className="container-scroller">
            <div className="container-fluid page-body-wrapper full-page-wrapper">
                <div className="content-wrapper d-flex align-items-center auth">
                    <div className="row w-100">
                        <div className="col-lg-4 mx-auto">
                            <div className="auth-form-light text-left p-5">
                                <h2>Se connecter</h2>
                                <form className="pt-3">
                                    <div className="form-group">
                                        <input type="email" onChange={(e)=>getInputedValue(e, setEmail)} className="form-control form-control-lg" id="exampleInputEmail1" placeholder="email" />
                                    </div>
                                    <div className="form-group">
                                        <input type="password" onChange={(e)=>getInputedValue(e, setPwd)} className="form-control form-control-lg" id="exampleInputPassword1" placeholder="mot de passe" />
                                    </div>
                                    <div className="mt-3">
                                        <button type="button" onClick={login} className="btn btn-block btn-primary btn-lg font-weight-medium auth-form-btn" disabled={disable}>
                                            CONNEXION
                                        </button>
                                    </div>
                                    <div className="my-2 d-flex justify-content-between align-items-center">
                                        <div className="form-check">
                                            <label className="form-check-label text-muted">
                                                <input type="checkbox" className="form-check-input" />
                                                Rester connecté
                                            </label>
                                        </div>
                                        <button type="button" className="btn auth-link text-black">Mot de passe oublié?</button>
                                    </div>
                                    <div className="text-center mt-4 font-weight-light">
                                        Pas de compte? <a href="/signin" className="text-primary">Créer</a>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}