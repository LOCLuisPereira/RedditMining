import styled,{css} from 'styled-components'
import {useState, useEffect} from 'react'

/*
FUNCTION TO SEND DATA TO THE FASTAPI SERVER
*/
const send = async (props) => {
  const res = await fetch(
    `http://127.0.0.1:8000/snd_subreddit_list`,{
      method : 'POST',
      headers : {
        'Content-Type' : 'application/json',
      },
      body : JSON.stringify(props),
    })
}

/*
TRANSFORM DATA RECEIVED FROM THE SERVER TO FIT REACT'S STATE MECHANISM
*/
const transform = (data) => {
  var xs = {}
  data.forEach(
    x => xs[x.name] = x.status
  )
  return xs
}

const MainContainer = styled.div`
  padding: 0.01rem;
  background-color: #F7F4EA;
  width:100wh;
  height:100vh;
  overflow: scroll
`

const Banner = styled.div`
  background-color: #DED9E2;
  margin-top: 2rem;
  margin-left: 2rem;
  margin-right: 2rem;
  border-style: solid;
  border-width: 0.1rem;
  box-shadow: 15px 15px;
`

const Title = styled.p`
  font-family: Georgia, serif;
  font-size: 3.5rem;
  text-align:center;
`

const Container = styled.div.attrs(props => ({
  status: props.status?'#75C9C8':'#C0B9DD' || '#C0B9DD',
}))`
  background-color: ${props=>props.status};
  border-style: solid;
  border-width: 0.1rem;
  margin-top: 2rem;
  margin-left: 15rem;
  margin-right: 15rem;
  box-shadow: 10px 10px;
`
const ContainerButton = styled.div`
  background-color: #DED9E2;
  border-style: solid;
  border-width: 0.1rem;
  margin-top: 2rem;
  margin-left: 8rem;
  margin-right: 8rem;
  box-shadow: 10px 10px;
`

const ContainerButtonText = styled.p`
  font-family: Georgia, serif;
  font-size: 1.5rem;
  text-align:center;
`

const ContainerText = styled.p`
  font-family: Georgia, serif;
  font-size: 1.5rem;
  text-align:center;
  `

const ContainerList = styled.ul`
  list-style-type: none;
`

const ContainerInputFilter = styled.div`
  margin-top: 2rem;
  margin-left: 10rem;
  margin-right: 10rem;
  border-style: solid;
  border-width: 0.1rem;
  box-shadow: 5px 5px;

  `

const InputFilter = styled.input`
  background-color: #DED9E2;

  font-family: Georgia, serif;
  font-size: 1.5rem;
  text-align:center;

  max-width: 100vw;
  max-height: 100vh;
  width: 100%;
  height: 100%;

  border-width: 0rem;

  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
`


/* MAIN COMPONENT */
/*
Note, forceUpdate and everything related to it, it a tricky clever method.
To force component refreshment. This allows changing the style...
Otherwise, it would be impossible.
*/
const Home = (props) => {
  const [subs, setSubs] = useState(transform(props.subredditList))
  const [subFilter, setSubFilter] = useState('')
  const [xs, forceUpdate] = useState({})

  const stateUpdate = (event, name) => {
    subs[name] = !subs[name]
    forceUpdate({...xs})

  }

  return (
    <MainContainer>

      <Banner>
        <Title>Subreddit Mining List</Title>
      </Banner>

      <ContainerButton onClick={() => send(subs)}>
        <ContainerButtonText>Update Mining List</ContainerButtonText>
      </ContainerButton>

      <ContainerInputFilter onChange={(e) => setSubFilter(e.target.value)}>
        <InputFilter placeholder='Write Subreddit Filter...'/>
      </ContainerInputFilter>

      <ContainerList>
        {props.subredditList
          .filter( x => x.name.toLowerCase().includes(subFilter.toLowerCase()) )
          .map(x => { return (
          <li key={x.name}>
            <Container status={subs[x.name]} onClick={(e) => stateUpdate(e,x.name)}>
              <ContainerText>{x.name}</ContainerText>
            </Container>
          </li>
        )})}
      </ContainerList>

    </MainContainer>
  )
}


/*
FETCH DATA FROM THE SERVER AND PASSES IT INTO THE
HOME COMPONENT.
*/
export const getServerSideProps = async (context) => {
  const data = await fetch('http://127.0.0.1:8000/rcv_subreddit_list')
  const res = await data.json()

  return {
    props : res
  }

}




export default Home