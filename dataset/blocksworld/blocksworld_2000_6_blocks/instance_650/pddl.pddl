

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b c)
(ontable c)
(on d a)
(on e b)
(clear d)
(clear e)
)
(:goal
(and
(on a d)
(on c b)
(on d c))
)
)


