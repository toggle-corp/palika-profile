const cellRendererParams = ({ datum, column: { key } }) => ({
    value: datum[key],
});

const headerRendererParams = ({ column }) => ({
    value: column.key,
});

const Header = ({ value }) => value;

const Cell = ({ value }) => value;

const columns = [
    {
        key: 'index',

        headerRendererParams,
        cellRendererParams,

        headerRenderer: Header,
        cellRenderer: Cell,
    },
    {
        key: 'column',

        headerRendererParams,
        cellRendererParams,

        headerRenderer: Header,
        cellRenderer: Cell,
    },
    {
        key: 'message',

        headerRendererParams,
        cellRendererParams,

        headerRenderer: Header,
        cellRenderer: Cell,
    },
];

export default columns;
