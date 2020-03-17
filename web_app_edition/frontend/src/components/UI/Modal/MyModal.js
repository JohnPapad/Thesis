import React from 'react';
import { Button, Modal, ModalHeader, ModalBody, ModalFooter } from 'reactstrap';

const myModal = (props) => {
    
    let modal_header = null;
    if (props.modalHeader)
    {
        modal_header = (
            <ModalHeader toggle={props.modalClosed} className={props.modalHeader["classes"].join(' ')}>
                {props.modalHeader["title"]}
            </ModalHeader> 
        ) ;
    }

    let modal_body = null;
    if (props.modalBody)
    {
        modal_body = (
            <ModalBody className={props.modalBody["classes"].join(' ')}>
                {props.modalBody["content"]}
            </ModalBody> 
        ) ;
    }

    let modal_footer = null;
    if (props.modalFooter)
    {
        const modal_footer_content = (
            <>
            <Button color="primary" onClick={props.toggle}>Do Something</Button>{' '}
            <Button color="secondary" onClick={props.toggle}>Cancel</Button> 
            </>
        );
        modal_footer = (
            <ModalFooter className={props.modalFooter["classes"].join(' ')}>
                {modal_footer_content}
            </ModalFooter>
        );
    }

    return (
        <Modal isOpen={props.showModal} toggle={props.modalClosed} className={props.className}>
            {modal_header}
            {modal_body}
            {modal_footer}
        </Modal>
    );
}


export default myModal;