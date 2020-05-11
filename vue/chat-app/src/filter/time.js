export default (value) => {
    print(value)
    let time = value.toJSON().slice(0,16).replace(/-/g,'/');
    print(time)
    return time.toString();
}