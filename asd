try {
        curlpp::Easy request;

        request.setOpt(new curlpp::options::Url("https://graphql.anilist.co")); 
        request.setOpt(new curlpp::options::Verbose(true)); 
        
        std::list<std::string> header;
        header.push_back("Content-Type: application/json");

        std::string post = "{\"query\": \"query{Activity(id:26266744) { __typename ... on TextActivity{ text, replies { text }}}}\"}";
        //header.push_back(post);

        request.setOpt(new curlpp::options::HttpHeader(header)); 
        request.setOpt(new curlpp::options::PostFields(post));
        request.setOpt(new curlpp::options::PostFieldSize(1 + post.length()));
        // request.setOpt(new curlpp::options::(post));
        //request.setOpt(curlpp::options:: (post));
        //std::cout << request.getHandle();
        //std:istream req;
        request.perform();
        //req << request;
    }
    catch ( curlpp::LogicError & e ) {
        std::cout << e.what() << std::endl;
    }
    catch ( curlpp::RuntimeError & e ) {
        std::cout << e.what() << std::endl;
    }

    return EXIT_SUCCESS;
