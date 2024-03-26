

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(on c b)
(on d c)
(on e a)
(clear e)
)
(:goal
(and
(on b c)
(on c a)
(on d e)
(on e b))
)
)


