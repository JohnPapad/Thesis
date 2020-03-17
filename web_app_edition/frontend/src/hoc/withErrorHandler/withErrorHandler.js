import React, { Component } from 'react';

import MyModal from '../../components/UI/Modal/MyModal';

const withErrorHandler = ( WrappedComponent, axios ) => {
    return class extends Component {
        state = {
            error: null
        }

        componentWillMount () {
            this.reqInterceptor = axios.interceptors.request.use( req => {
                this.setState( { error: null } );
                return req;
            } );
            this.resInterceptor = axios.interceptors.response.use( res => res, error => {
                this.setState( { error: error } );
            } );
        }

        componentWillUnmount () {
            axios.interceptors.request.eject( this.reqInterceptor );
            axios.interceptors.response.eject( this.resInterceptor );
        }

        errorConfirmedHandler = () => {
            this.setState( { error: null } );
        }

        render () {
            return (
                <>
                    <MyModal 
                        showModal = {this.state.error ? true : false}
                        modalClosed = {this.errorConfirmedHandler}
                        modalBody = {this.state.error ? {content : this.state.error.message, classes : []} : null}
                    />
                    <WrappedComponent {...this.props} />
                </>
            );
        }
    }
}

export default withErrorHandler;