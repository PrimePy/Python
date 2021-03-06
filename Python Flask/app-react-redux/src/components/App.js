import React from 'react';
import {Route, Switch} from 'react-router-dom';
import HomePage from './home/HomePage';
import AboutPage from './about/AboutPage';
import TechPage from './tech/TechPage';
import ManageTechPage from './tech/ManageTechPage';
import Header from './common/Header';
import PageNotFound from './PageNotFound';
import { ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const App = ()=> (
	<div className="container-fluid">
		<Header/>
		<Switch>
			<Route exact path="/" component={HomePage}/>
			<Route path="/about" component={AboutPage}/>
			<Route path="/tech" component={TechPage}/>
			<Route path="/get-tech/:id" component={ManageTechPage}/>
			<Route path="/get-tech" component={ManageTechPage}/>
			<Route  component={PageNotFound}/>
		</Switch>
		<ToastContainer autoClose={3000} hideProgressBar/> 
	</div>
	);

export default App;
