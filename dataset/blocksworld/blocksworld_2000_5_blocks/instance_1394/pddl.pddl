

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a e)
(ontable b)
(ontable c)
(on d a)
(on e c)
(clear b)
(clear d)
)
(:goal
(and
(on c b)
(on d e)
(on e c))
)
)


