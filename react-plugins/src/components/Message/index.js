import PropTypes from 'prop-types';
import React from 'react';

import { connect } from '../../storage';

import styles from './styles.scss';


const mapStateToProps = state => ({
    suffix: state.suffix,
});

@connect(mapStateToProps)
export default class Message extends React.PureComponent {
    static propTypes = {
        className: PropTypes.string,
        message: PropTypes.string.isRequired,
        suffix: PropTypes.string,
    }

    static defaultProps = {
        className: '',
        suffix: '',
    }

    componentDidMount() {
        console.log('mounting');
    }

    getClassName = () => {
        const { className } = this.props;
        const classNames = [
            className,
            styles.message,
        ];

        return classNames.join(' ');
    }

    render() {
        console.log('rerendering');

        return (
            <div className={this.getClassName()}>
                { this.props.message }
                &nbsp;
                { this.props.suffix }
            </div>
        );
    }
}
