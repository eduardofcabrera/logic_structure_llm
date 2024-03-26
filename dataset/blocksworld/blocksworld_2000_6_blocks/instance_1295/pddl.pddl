

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a c)
(ontable b)
(on c b)
(on d a)
(ontable e)
(clear d)
(clear e)
)
(:goal
(and
(on a d)
(on b c)
(on e b))
)
)


