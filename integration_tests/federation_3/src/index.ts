import {ApolloServer} from 'apollo-server'
import {ApolloGateway} from '@apollo/gateway'

const serviceA_url: string = 'http://service_3_a:5003/graphql/';
const serviceB_url: string = 'http://service_3_b:5003/graphql/';
const serviceC_url: string = 'http://service_3_c:5003/graphql/';
const serviceD_url: string = 'http://service_3_d:5003/graphql/';

const gateway = new ApolloGateway({
    serviceList: [
        { name: 'service_3_a', url: serviceA_url },
        { name: 'service_3_b', url: serviceB_url },
        { name: 'service_3_c', url: serviceC_url },
        { name: 'service_3_d', url: serviceD_url },
    ],
});

const server = new ApolloServer({
    gateway,
    subscriptions: false
});

server.listen(3003).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
