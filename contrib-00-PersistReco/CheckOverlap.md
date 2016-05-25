```C++
//===========================================================================
// Check duplicate entries
//===========================================================================
bool CheckOverlap::searchOverlap( std::vector<const LHCb::ProtoParticle* > & proto )
{
  if (msgLevel(MSG::VERBOSE)) verbose() << "searchOverlap(protos)" << endmsg ;
  // It its a simple particle made from protoparticle. Check.

  for (std::vector<const LHCb::ProtoParticle* >::const_iterator i = proto.begin();
       i != proto.end() ; ++i)
  {
    for (std::vector<const LHCb::ProtoParticle* >::const_iterator j = i ;
         j != proto.end(); ++j)
    {
      if (j==i) continue ;
      if ( *i==*j )
      {
          if (msgLevel(MSG::VERBOSE)) verbose() << "Found overlap " << *i << endmsg ;
          return true ;
      }
      else {
        const std::vector<LHCb::LHCbID> i_ids = (*i)->track()->lhcbIDs();
        const std::vector<LHCb::LHCbID> j_ids = (*j)->track()->lhcbIDs();
        std::vector<LHCb::LHCbID> diff;
        std::set_symmetric_difference(i_ids.begin(), i_ids.end(), j_ids.begin(), j_ids.end(), std::back_inserter(diff));

        if (std::all_of(diff.begin(), diff.end(), [] (LHCb::LHCbID id) { return id.isCalo(); } ))
        {
          if (msgLevel(MSG::VERBOSE)) verbose() << "Found overlap using LHCb IDs, ignoring isCalo IDs" << *i << endmsg ;
          return true;
        }
      }
     }
  }
  if (msgLevel(MSG::VERBOSE)) verbose() << "Found no overlap" << endmsg ;
  return false;
}
```
