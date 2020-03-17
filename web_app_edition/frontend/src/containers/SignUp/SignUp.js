import React from 'react';
import produce from 'immer';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import axios from '../../Services/axiosConfig';
import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler';
import classes from './SignUp.module.scss';
import { Form, Card, CardHeader, CardBody, Row, Col, Button} from 'reactstrap';
import MyInput from '../../components/UI/MyInput/MyInput';
import { API } from '../../Services/API';   
import * as actions from '../../store/actions/index';
import { checkValidity } from '../../Utilities/validityUtility';


class SignUp extends React.Component {

    state = {
        formControls: {
            email: {
                rules: {
                    required: true,
                    isEmail: true
                },
                id: "signup_user_email",
                name: "Email",
                value: '',
                type: "text",
                placeholder: "example@example.com",
                feedback: null,
                validity: ''
            },

            password: {
                rules: {
                    required: true,
                    isPassword: true,
                    minLength: 8,
                    maxLength: 15
                },
                id: "signup_user_pwd",
                name: "Password",
                value: '',
                type: "password",
                placeholder: 'Password',
                feedback: null,
                validity: ''
            },

            password1: {
                rules: {
                    required: true,
                    mustMatch: "password"
                },
                id: "signup_user_pwd_rep",
                name: "Confirm Password",
                value: '',
                type: "password",
                placeholder: 'Confirm Password',
                feedback: null,
                validity: ''
            },

            username: {
                rules: {
                    required: true,
                    onlyLettersDotsAndSpace: true,
                    minLength: 2,
                    maxLength: 15
                },
                id: "signup_user_username",
                name: "Username",
                value: '',
                type: "text",
                placeholder: "username",
                feedback: null,
                validity: ''
            },

            first_name: {
                rules: {
                    required: true,
                    onlyLetters: true,
                    minLength: 2,
                    maxLength: 20
                },
                id: "signup_user_name",
                name: "Name",
                value: '',
                type: "text",
                placeholder: "Name",
                feedback: null,
                validity: ''
            },

            last_name: {
                rules: {
                    required: true,
                    onlyLetters: true,
                    minLength: 2,
                    maxLength: 20
                },
                id: "signup_user_surname",
                name: "Surname",
                value: '',
                type: "text",
                placeholder: "Surname",
                feedback: null,
                validity: ''
            }
        }
    }

    //---------------------Form Manipulation------------------------

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

    checkEmailValidity = () => {
        API.checkEmailValidity(axios, this.state.formControls.email.value).then(res => {
            if (!res)
            {
                return;
            }

            if (!res.success)
            {
                this.setFormField("email", null, 'is-valid', null);
            }
            else
            {
                this.setFormField("email", "This email address is connected with an existing account", 'is-invalid', null);
            }
        });
    }

    checkUsernameValidity = () => {
        API.checkUsernameValidity(axios, this.state.formControls.username.value).then(res => {
            if (!res)
            {
                return;
            }

            if (!res.success)
            {
                this.setFormField("username", null, 'is-valid', null);
            }
            else
            {
                this.setFormField("username", "Username is taken", 'is-invalid', null);
            }
        });
    }

    inputBlurredHandler = ( event, controlName ) => {
        if ((controlName === "email") && (this.state.formControls.email.validity !== "is-invalid") && (this.state.formControls.email.value.trim() !== '' ))
        {
            this.checkEmailValidity();
        }
        else if ((controlName === "username") && (this.state.formControls.username.validity !== "is-invalid") && (this.state.formControls.username.value.trim() !== '' ))
        {
            this.checkUsernameValidity();
        }
        else if ((controlName === "password1") && (this.state.formControls.password1.validity !== "is-invalid") && (this.state.formControls.password1.value.trim() !== '' ))
        {
            if (this.state.formControls.password.value !== this.state.formControls.password1.value)
            {
                this.setFormField("password1", "Passwords don't match", "is-invalid", null);
            }
            else if (this.state.formControls.password.validity !== "is-invalid")
            {
                this.setFormField("password1", null, "is-valid", null);
            }
        }
        else if ((controlName === "password") && (this.state.formControls.password1.value.trim() !== ''))
        {
            if (this.state.formControls.password.value !== this.state.formControls.password1.value)
            {
                this.setFormField("password1", "Passwords don't match", "is-invalid", null);
            }
            else
            {
                this.setFormField("password1", null, "is-valid", null);
            }
        }
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
            if ((controlName === "password1") || (controlName === "email"))
            { 
                this.setFormField(controlName, null, '', null);
            }
            else
            {
                this.setFormField(controlName, null, 'is-valid', null);
            }
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
            formData[key] = this.state.formControls[key].value;

            if (this.state.formControls[key].validity === "is-valid")
            {
                continue;
            }

            if (this.state.formControls[key].validity === "is-invalid")
            {
                formIsValid = false;
                continue;
            }

            const res = checkValidity(this.state.formControls[key].value, this.state.formControls[key].rules);
            if (!res.report)
            {
                formIsValid = false;
                errFeedBack[key] = res.msg;
            }
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

        API.signUp(axios, formData).then(res => {
            if (!res)
            {
                return;
            }
                    
            if (!res.success)
            {
                if (res.data.message === "Sign up error: email is already taken")
                {
                    this.setFormField("email", "This email address is connected with an existing account", 'is-invalid', null);
                }
                else if (res.data.message === "Sign up error: mismatching password")
                {
                    this.setFormField("password1", "Passwords don't match", "is-invalid", null);
                }
            }
            else
            {
                this.props.onSignUpSuccess(res.data.token, res.data.userId, res.data.username);
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
                blurred={( event ) => this.inputBlurredHandler ( event, formElement.id )}
            />
        ));

        return (
            <Row id={classes.content}> 
                <Col xs="12" id={classes.bg_gradient}>
                    <Row className="justify-content-center pb-5">
                        <Col className="align-self-center" xs="12" sm="10" md="9" lg="6" style={{paddingRight: "10%", paddingLeft: "10%"}}>
                            <Card id={classes.signup_form}>
                                <CardHeader id={classes.header}>
                                    Sign Up
                                </CardHeader>

                                <CardBody>
                                    
                                    <p id={classes.form_text} className="small ">Sign Up to gain full access to all features.</p>

                                    <Form onSubmit={this.submitHandler}>
                                        {formFields}
                                        <Button className="float-right mt-3" id={classes.submit_btn}>
                                            <span style={{textShadow: "2px 2px 2px black"}}>
                                                Sign Up
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
        onSignUpSuccess: (token, userId, username) => dispatch(actions.authSuccess(token, userId, username))
    }
}

export default connect(null, mapDispatchToProps)(withErrorHandler( withRouter(SignUp), axios ));