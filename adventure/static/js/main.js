'use strict';

const csrftoken = Cookies.get('csrftoken');

const get_top_list = async () => {
    let topUsers = await fetch("/api/top/")
        .then(res => res.json())
        .then(customers => customers.response);
    await console.log(topUsers)
    return topUsers;
};

const create_tran = async (file) => {
    const formData = new FormData()
    formData.append('tfile', file)

    await fetch("/api/create/", {
        method: 'POST',
        headers: {
            // 'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW',
            "X-CSRFToken": csrftoken,
        },
        body: formData,
    }).then(res => res.json())
        .then(mess => alert(`Uploaded: ${mess["upload success"]}`));
};

// const detail_tran = async (tran_id) => {
//     await fetch(`/api/detail/${tran_id}`)
//         .then(res => res.json())
//         .then(trans => trans);
// };

// const delete_tran = async (tran_id) => {
//     await fetch(`/api/detail/${tran_id}/`, {
//         method: 'DELETE',
//         headers: {
//             "X-CSRFToken": csrftoken,
//         }
//     });
// };

// const update_tran = async (tranId, tran) => {
//     await fetch(`/api/detail/${tranId}/`, {
//         method: 'PUT',
//         headers: {
//             'Content-Type': 'application/json;charset=utf-8',
//             "X-CSRFToken": csrftoken,
//         },
//         body: JSON.stringify({
//             "task": tran
//         })
//     });
// };

const App = () => {
    const [topList, setTopList] = React.useState([]);
    const [refresh, setRefresh] = React.useState(false);

    React.useEffect(()=>{
        let topList = get_top_list();
        topList.then(data => setTopList(data));
    }, [refresh]);

    return (
        <div>
            <Dashboard />

            <div>
                <button onClick={()=>{get_top_list(); setRefresh(!refresh)}}
                        className="btn btn-primary ">Get Top #5 <br/>(Refresh)</button>
            </div>

            {topList.length > 0 &&
                <div className="d-grid gap-3">
                    <h4 className="mb-3 mt-5">List of Top #5 Customers</h4>
                    {topList.map((item, ind)=>{
                        return <CustomerItem item={item} key={ind+3} id={item.id} />
                    })}
                </div>
            }

        </div>
    )
};


const Dashboard = ()=>{
    const fileInput = React.createRef();
    const handleSubmit = (event) => {
        event.preventDefault();
        create_tran(fileInput.current.files[0]);
    }
    return(
        <form method='post' encType="multipart/form-data" id="formDash">
            <div className="input-group mb-3">
                <input type="file" className="form-control" placeholder="Input .csv file"
                       accept="text/csv" ref={fileInput}/>
                <button className="btn btn-secondary" type="button" id="button-addon2"
                        onClick={(event) =>handleSubmit(event)}>Upoad</button>
            </div>
        </form>
    )
};

const CustomerItem = ({item, id, toRefresh})=>{
    return (
        <div className="col border border-secondary border-2 p-2 rounded">
            <div className="row pe-2">

                <div className="col">
                    <h5 className="title">{item.username}</h5>
                    <p className="h6">Total Spent Money: {item.spent_money}</p>
                    <p className="h6">Gems: {item.gems}</p>
                    <p className="h6">{new Date(item.date).toLocaleDateString()} {new Date(item.date).toLocaleTimeString()}</p>
                </div>

            </div>
        </div>
    )
};


ReactDOM.render(<App/>, document.getElementById('root'));