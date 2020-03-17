import React from 'react';
import produce from 'immer';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import axios from '../../Services/axiosConfig';
import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler';
import classes from './SignIn.module.scss';
import { Card, CardHeader, CardBody, Row, Col, Form, Alert, Button} from 'reactstrap';
import MyInput from '../../components/UI/MyInput/MyInput';
import { checkValidity } from '../../Utilities/validityUtility';
import { API } from '../../Services/API'; 
import * as actions from '../../store/actions/index';

    
class SignIn extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            formControls: {
                username: {
                    rules: {
                        required: true
                    },
                    id: "login_username",
                    name: "Username",
                    value: '',
                    type: "text",
                    placeholder: "",
                    feedback: null,
                    validity: ''
                },

                password: {
                    rules: {
                        required: true
                    },
                    id: "login_pwd",
                    name: "Password",
                    value: '',
                    type: "password",
                    placeholder: '',
                    feedback: null,
                    validity: ''
                }
			},
			alert:{
				visible: false,
				message: ''
			}
        };
    }
    
    onDismiss = () => {
		this.setState(
			produce( draft => {
				draft.alert.visible = false;
			})
		)
    }
    
    setFormField = (controlName, feedback, validity, value) => {
        this.setState(
            produce(draft => {
                draft.formControls[controlName].feedback = feedback;
                draft.formControls[controlName].validity = validity;
                if (value)
                {
                    draft.formControls[controlName].value = value;
                }
            })
        );
    }

    setFormWithError = () => {
        this.setState(
            produce(draft => {
                draft.formControls.password.value = '';
                draft.formControls.password.feedback = null;
                draft.formControls.password.validity = "is-invalid";
          
                draft.formControls.username.value = '';
                draft.formControls.username.feedback = null;
                draft.formControls.username.validity = "is-invalid";
            })
        );
    }

    inputChangedHandler = ( event, controlName ) => {

        const value = event.target.value;
        this.setState( 
            produce(draft => { 
                draft.formControls[controlName].value = value; 
            }) 
        ); 

        const res = checkValidity(value, this.state.formControls[controlName].rules);
        if (res.report)
        {
            this.setFormField(controlName, null, '', null);
        }
        else
        {
            this.setFormField(controlName, res.msg, "is-invalid", null);
        }       
    }
    
    submitHandler = ( event ) => {
        event.preventDefault();

        let formData = {};
        let formIsValid = true;
        let errFeedBack = {};
        for ( let key in this.state.formControls ) 
        {
            const res = checkValidity(this.state.formControls[key].value, this.state.formControls[key].rules);
            if (!res.report)
            {
                formIsValid = false;
                errFeedBack[key] = res.msg;
            }
            formData[key] = this.state.formControls[key].value;
        }

        if (!formIsValid)
        {
            this.setState(
                produce(draft => {
                    for ( let key in errFeedBack ) 
                    {
                        draft.formControls[key].feedback = errFeedBack[key];
                        draft.formControls[key].validity = "is-invalid";
                    }
                })
            );
            return;
        }

        API.signIn(axios, formData).then(res => {
            if (!res) 
            {
                return;
            }

            if (!res.success)
            {
				this.setFormWithError();
				this.setState(
					produce( draft => {
						draft.alert.message = "Wrong credentials. Please try again";
						draft.alert.visible = true;
					})
				)
            }
            else
            {
                this.props.onSignInSuccess(res.data.token, res.data.userId, res.data.username);
                this.props.history.replace("/");
            }
        });
    }

    
    render(){

        const formElementsArray = [];
        for ( let key in this.state.formControls ) 
        {
            formElementsArray.push( {
                id: key,
                config: this.state.formControls[key]
            });
        }

        let formFields = formElementsArray.map( formElement => (
            <MyInput
                key={formElement.id}
                id={formElement.config.id}
                name={formElement.config.name}
                value={formElement.config.value}
                type={formElement.config.type}
                placeholder={formElement.config.placeholder}
                feedback={formElement.config.feedback}
                validity={formElement.config.validity}
                changed={( event ) => this.inputChangedHandler( event, formElement.id )} 
            />
        ));

        return (            
            <Row id={classes.content}> 
                <Col xs="12" id={classes.bg_gradient}>
                    <Row className="justify-content-center">
                        <Alert 
                                color="danger" 
                                isOpen={this.state.alert.visible} 
                                toggle={() => (this.onDismiss())}
                        >
                            {this.state.alert.message}
                        </Alert>
                    </Row>
                    <Row className="justify-content-center">
                        <Col className="align-self-center" xs="12" sm="8" md="6" lg="5" style={{paddingLeft : "10%", paddingRight: "10%"}}>
                            <Card id={classes.login_form}>
                                <CardHeader id={classes.header}>
                                    Sign In
                                </CardHeader>

                                <CardBody>
                                    
                                    <p id={classes.form_text} className="small ">Sign In using your existing account to have full access to all features.</p>

                                    <Form onSubmit={this.submitHandler}>
                                        {formFields}
                                        <Button className="float-right mt-3" id={classes.submit_btn}>
                                            <span style={{textShadow: "2px 2px 2px black"}}>
                                                Sign In
                                            </span>
                                        </Button>
                                    </Form>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                </Col>
            </Row>
        );
    }

}


const mapDispatchToProps = dispatch => {
    return {
        onSignInSuccess: (token, userId, username) => dispatch(actions.authSuccess(token, userId, username))
    }
}

export default connect(null, mapDispatchToProps)(withErrorHandler( withRouter(SignIn), axios ));
