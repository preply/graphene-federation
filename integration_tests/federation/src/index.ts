import {ApolloServer} from 'apollo-server'
import {ApolloGateway} from '@apollo/gateway'

const serviceA_url: string = 'http://service_a:5000/graphql';

const gateway = new ApolloGateway({
    serviceList: [
        { name: 'service_a', url: serviceA_url },
    ],
});

const server = new ApolloServer({
    gateway,
    subscriptions: false
});

server.listen(3000).then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
