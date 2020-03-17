
// Dynamically rendered component
const DRC = (props) => {
    if (props.renderFlag)
    {
        return props.children ;
    }
    else
    {
        return null ;
    }
}

export default DRC;